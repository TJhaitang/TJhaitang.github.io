---
title: Vue学习笔记
date: 2021-10-26 17:58:59
tags: '普罗米修斯'
categories: '数据库大作业'
---
## Reference
- [Vue教程-菜鸟教程](https://www.runoob.com/vue3/vue3-tutorial.html)
## Vue是什么？
不知道

## Vue能做的事情

## Vue功能实例
- 目录

|||||||
|:--:|:--:|:--:|:--:|:--:|:--:|
[Hello World](#Hello-World)|[v-once](#v-once)|[v-html](#v-html)|[v-bind](#v-bind)|[v-model](#v-model)|[v-on](#v-on)
[v-if](#v-if)|[v-for](#v-for)|[vue组件](#vue组件)|[Prop](#Prop)|[computed](#computed)

### Hello World
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Vue 测试实例1</title>
<script src="https://unpkg.com/vue@next"></script>
</head>
<body>
<div id="hello-world" class="demo">
  {{ message }}
</div>

<script>
const HelloVueApp = {
  data() {
    return {
      message: 'Hello World!!'
    }
  }
  //这是HelloVueApp这个VueApp中的成员函数，使用Js语法
  methods:{
      Bye(){
          this.message='Bye World!'
      }
  }
}

Vue.createApp(HelloVueApp).mount('#hello-world')
</script>
</body>
</html>
```
### v-once
```html
<body>
    <div id='test'>
        <span v-once>
            {{message}}
            </span>
    </div>

    <script>
        const OnceTest={
            data(){
                return{
                    message:'hello world'
                }
            }
        }
        Vue.createApp(OnceTest).mount('#test')
        message='Bye world'//span中的内容不发生改变
    </script>
</body>
```
### v-html
```html
<body>
<div id="example1" class="demo">
    <!--这里会输出字符串-->
    <p>使用双大括号的文本插值: {{ rawHtml }}</p>
    <!--这里会输出html结果-->
    <p>使用 v-html 指令: <span v-html="rawHtml"></span></p>
</div>

<script>
const RenderHtmlApp = {
  data() {
    return {
      rawHtml: '<span style="color: red">这里会显示红色！</span>'
    }
  }
}

Vue.createApp(RenderHtmlApp).mount('#example1')
</script>
</body>
```

### v-bind
- 将变量绑定
```html
<div id="app">
    <!--这里用到了v-model指令，这是双向绑定指令，将会在后面体现-->
  <label for="r1">修改颜色</label><input type="checkbox" v-model="use" id="r1">
  <br><br>
  <!--通过use的值决定这个div的样式-->
  <!-- v-bind:class也可以简写为 :class -->
  <div v-bind:class="{'class1': use}">
    v-bind:class 指令
  </div>
</div>
    
<script>
const app = {
  data() {
    return {
      use: false
    }
  }
}
 
Vue.createApp(app).mount('#app')
</script>
```

### v-model
```html
<div id="app">
    <p>{{ message }}</p>
    <input v-model="message">
</div>
 
<script>
const app = {
  data() {
    return {
      message: 'Runoob!'
    }
  }
}
 
Vue.createApp(app).mount('#app')
</script>
```

### v-on
```html
<!-- 完整语法 -->
<a v-on:click="doSomething"> ... </a>

<!-- 缩写 -->
<a @click="doSomething"> ... </a>

<!-- 动态参数的缩写 (2.6.0+) -->
<a @[event]="doSomething"> ... </a>
```

### v-if
- v-if后的表达式决定这个元素是否展示
- 若要包括多个元素，可以使用`<template>`标签
```html
<div id="app">
    <div v-if="type === 'A'">
         A
    </div>
    <div v-else-if="type === 'B'">
      B
    </div>
    <div v-else-if="type === 'C'">
      C
    </div>
    <div v-else>
      Not A/B/C
    </div>
</div>
    
<script>
const app = {
  data() {
    return {
      type: "C" 
    }
  }
}
 
Vue.createApp(app).mount('#app')
</script>
```

### v-for
- `v-for`指令需要"site in sites"形式的语法
```html
<div id="app">
  <ul>
      <!--key和index为额外提供的参数可作为键名和索引-->
      <!--in后面的也可以是一个computed中返回可用数据类型的函数-->
    <li v-for="(value, key, index) in object">
     {{ index }}. {{ key }} : {{ value }}
    </li>
  </ul>
</div>
 
<script>
const app = {
  data() {
    return {
      object: {
        name: '菜鸟教程',
        url: 'http://www.runoob.com',
        slogan: '学的不仅是技术，更是梦想！'
      }
    }
  }
}
 
Vue.createApp(app).mount('#app')
</script>
```
### vue组件
```html
<!--全局组件-->
<div id="app">
    <button-counter></button-counter>
</div>

<script>
// 创建一个Vue 应用
const app = Vue.createApp({})

// 定义一个名为 button-counter 的新全局组件
app.component('button-counter', {
  data() {
    return {
      count: 0
    }
  },
  template: `
    <button @click="count++">
      点了 {{ count }} 次！
    </button>`
})
app.mount('#app')
</script>
```
```html
<!--局部组件-->
<div id="app">
    <runoob-a></runoob-a>
</div>
<script>
var runoobA = {
  template: '<h1>自定义组件!</h1>'
}
 
const app = Vue.createApp({
  components: {
    'runoob-a': runoobA
  }
})
 
app.mount('#app')
</script>
```
### Prop
```html
<div id="app">
  <site-name title="Google"></site-namet>
  <site-name title="Runoob"></site-namet>
  <site-name title="Taobao"></site-name>
</div>
 
<script>
const app = Vue.createApp({})
 
app.component('site-name', {
    //需要通过props显式的声明
    //将title传给template
  props: ['title'],
  template: `<h4>{{ title }}</h4>`
})
 
app.mount('#app')
</script>
```
- 动态Prop
```html
<div id="app">
  <site-info
    v-for="site in sites"
    :id="site.id"
    :title="site.title"
  ></site-info>
</div>
 
<script>
const Site = {
  data() {
    return {
      sites: [
        { id: 1, title: 'Google' },
        { id: 2, title: 'Runoob' },
        { id: 3, title: 'Taobao' }
      ]
    }
  }
}
 
const app = Vue.createApp(Site)
 
app.component('site-info', {
  props: ['id','title'],
  template: `<h4>{{ id }} - {{ title }}</h4>`
})
 
app.mount('#app')
</script>
```
- Prop验证
```javascript
Vue.component('my-component', {
  props: {
    // 基础的类型检查 (`null` 和 `undefined` 会通过任何类型验证)
    propA: Number,
    // 多个可能的类型
    propB: [String, Number],
    // 必填的字符串
    propC: {
      type: String,
      required: true
    },
    // 带有默认值的数字
    propD: {
      type: Number,
      default: 100
    },
    // 带有默认值的对象
    propE: {
      type: Object,
      // 对象或数组默认值必须从一个工厂函数获取
      default: function () {
        return { message: 'hello' }
      }
    },
    // 自定义验证函数
    propF: {
      validator: function (value) {
        // 这个值必须匹配下列字符串中的一个
        return ['success', 'warning', 'danger'].indexOf(value) !== -1
      }
    }
  }
})
```

### computed
- 可以使用method，但computed性能更好
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Vue 测试实例 - 菜鸟教程(runoob.com)</title>
<script src="https://unpkg.com/vue@next"></script>
</head>
<body>
<div id="app">
  <p>原始字符串: {{ message }}</p>
  <p>计算后反转字符串: {{ reversedMessage }}</p>
</div>
    
<script>
const app = {
  data() {
    return {
      message: 'RUNOOB!!'
    }
  },
  computed: {
    // 计算属性的 getter
    reversedMessage: function () {
      // `this` 指向 vm 实例
      return this.message.split('').reverse().join('')
    }
  }
}
 
Vue.createApp(app).mount('#app')
</script>
```
- computed vs methods
```javascript
methods: {
  reversedMessage2: function () {
    return this.message.split('').reverse().join('')
  }
}
//我们可以使用 methods 来替代 computed，效果上两个都是一样的，但是 computed 是基于它的依赖缓存，只有相关依赖发生改变时才会重新取值。而使用 methods ，在重新渲染的时候，函数总会重新调用执行。
```
- computed setter
**还没学到**