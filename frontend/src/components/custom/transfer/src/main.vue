<template>
  <div class="el-transfer">
    <transfer-panel v-bind="$props"
                    ref="leftPanel"
                    :data="sourceData"
                    :title="titles[0] || t('el.transfer.titles.0')"
                    :default-checked="leftDefaultChecked"
                    :placeholder="filterPlaceholder || t('el.transfer.filterPlaceholder')"
                    @checked-change="onSourceCheckedChange">
      <slot name="left-footer"></slot>
    </transfer-panel>
    <div class="el-transfer__buttons">
      <el-button type="primary"
                 :class="['el-transfer__button', hasButtonTexts ? 'is-with-texts' : '']"
                 @click.native="addToLeft"
                 :disabled="rightChecked.length === 0">
        <i class="el-icon-arrow-left"></i>
        <span v-if="buttonTexts[0] !== undefined">{{ buttonTexts[0] }}</span>
      </el-button>
      <el-button type="primary"
                 :class="['el-transfer__button', hasButtonTexts ? 'is-with-texts' : '']"
                 @click.native="addToRight"
                 :disabled="leftChecked.length === 0">
        <span v-if="buttonTexts[1] !== undefined">{{ buttonTexts[1] }}</span>
        <i class="el-icon-arrow-right"></i>
      </el-button>
    </div>
    <transfer-panel v-bind="$props"
                    ref="rightPanel"
                    :data="targetData"
                    :title="titles[1] || t('el.transfer.titles.1')"
                    :default-checked="rightDefaultChecked"
                    :placeholder="filterPlaceholder || t('el.transfer.filterPlaceholder')"
                    @checked-change="onTargetCheckedChange">
      <slot name="right-footer"></slot>
    </transfer-panel>
  </div>
</template>

<script>
import ElButton from 'element-ui/packages/button'
import Emitter from 'element-ui/src/mixins/emitter'
import Locale from 'element-ui/src/mixins/locale'
import TransferPanel from './transfer-panel.vue'
import Migrating from 'element-ui/src/mixins/migrating'

export default {
  name: 'ElTransfer',

  mixins: [Emitter, Locale, Migrating],

  components: {
    TransferPanel,
    ElButton
  },

  props: {
    data: {
      type: Array,
      default() {
        return []
      }
    },
    titles: {
      type: Array,
      default() {
        return []
      }
    },
    buttonTexts: {
      type: Array,
      default() {
        return []
      }
    },
    filterPlaceholder: {
      type: String,
      default: ''
    },
    filterMethod: Function,
    leftDefaultChecked: {
      type: Array,
      default() {
        return []
      }
    },
    rightDefaultChecked: {
      type: Array,
      default() {
        return []
      }
    },
    renderContent: Function,
    value: {
      type: Array,
      default() {
        return []
      }
    },
    format: {
      type: Object,
      default() {
        return {}
      }
    },
    filterable: Boolean,
    props: {
      type: Object,
      default() {
        return {
          label: 'label',
          key: 'key',
          disabled: 'disabled'
        }
      }
    },
    targetOrder: {
      type: String,
      default: 'original'
    }
  },

  data() {
    return {
      leftChecked: [],
      rightChecked: []
    }
  },

  computed: {
    dataObj() {
      const key = this.props.key
      return this.data.reduce((o, cur) => (o[cur[key]] = cur) && o, {})
    },

    sourceData() {
      return this.data.filter(item => this.value.indexOf(item[this.props.key]) === -1)
    },

    targetData() {
      return this.targetOrder === 'original'
        ? this.data.filter(item => this.value.indexOf(item[this.props.key]) > -1)
        : this.value.map(key => this.dataObj[key])
    },

    hasButtonTexts() {
      return this.buttonTexts.length === 2
    }
  },

  watch: {
    value(val) {
      this.dispatch('ElFormItem', 'el.form.change', val)
    }
  },

  methods: {
    getMigratingConfig() {
      return {
        props: {
          'footer-format': 'footer-format is renamed to format.'
        }
      }
    },

    onSourceCheckedChange(val, movedKeys) {
      this.leftChecked = val
      if (movedKeys === undefined) return
      this.$emit('left-check-change', val, movedKeys)
    },

    onTargetCheckedChange(val, movedKeys) {
      this.rightChecked = val
      if (movedKeys === undefined) return
      this.$emit('right-check-change', val, movedKeys)
    },

    addToLeft() {
      const currentValue = this.value.slice()
      this.rightChecked.forEach(item => {
        const index = currentValue.indexOf(item)
        if (index > -1) {
          currentValue.splice(index, 1)
        }
      })
      this.$emit('input', currentValue)
      this.$emit('change', currentValue, 'left', this.rightChecked)
    },

    addToRight() {
      let currentValue = this.value.slice()
      const itemsToBeMoved = []
      const key = this.props.key

      // this.value是右边的值，左边选中的不可与右边的resource_name相同
      // selected集合的元素个数不小于权限个数，否则就说明有重复资源名
      this.same = true
      var selected = new Set()
      this.leftChecked.some(lc1 => {
        this.sourceData.some(sd1 => {
          if (sd1['key'] === lc1) {
            var cname = sd1['resource_name']
            selected.add(cname)
          }
        })
      })
      // 获取右边已选的resource_name
      var r_names = []
      this.value.some(v => {
        this.data.some(d => {
          if (d['key'] === v) {
            const res_name_r = d['resource_name']
            r_names.push(res_name_r)
          }
        })
      })

      if (this.leftChecked.length > selected.size) {
        this.same = false
        alert('不可同时选中资源名相同的权限')
      }
      // res 跳出循环
      var res = false
      this.leftChecked.some(lc => {
        this.sourceData.some(sd => {
          // 获取左边选中的resource_name
          if (sd['key'] === lc) {
            var res_name_l = sd['resource_name']
          }
          // 获取右边resource_name,和左边选中的作比较
          r_names.some(r => {
            if (r === res_name_l) {
              this.same = false
              res = true
              alert('用户组对同一资源不能分配多套权限')
              return true
            }
          })
          return res
        })
        return res
      })
      this.data.forEach(item => {
        const itemKey = item[key]
        if (
          this.leftChecked.indexOf(itemKey) > -1 &&
          this.value.indexOf(itemKey) === -1 && this.same
        ) {
          itemsToBeMoved.push(itemKey)
        }
      })
      currentValue = this.targetOrder === 'unshift'
        ? itemsToBeMoved.concat(currentValue)
        : currentValue.concat(itemsToBeMoved)
      this.$emit('input', currentValue)
      this.$emit('change', currentValue, 'right', this.leftChecked)
    },
    clearQuery(which) {
      if (which === 'left') {
        this.$refs.leftPanel.query = ''
      } else if (which === 'right') {
        this.$refs.rightPanel.query = ''
      }
    }
  }
}
</script>
