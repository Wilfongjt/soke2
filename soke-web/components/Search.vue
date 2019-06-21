<template>
  <div id="search" class="band">
    <h1 class="title">
      {{ page.title }}
    </h1>

    <form id="search" @submit.prevent="onSubmit">
      <p>
        <label for="form.words" class="subtitle">{{ page.subtitle }}</label>
      </p>
      <p>
        <input id="words" v-model="form.words" placeholder="words">
      </p>
      <p>
        <!-- span>
          <button class="button" type="button" @click="wordMe();">
            Word Me
          </button>
        </span -->
        <span>
          <button :disabled="form.submitStatus === 'PENDING'" class="button" type="submit">
            Submit!
          </button>
        </span>
      </p>
    </form>
    <ul id="search-results">
      <li v-for="item in page.items" :key="item.id">
        <span>{{ item }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { AWSHandlers } from './mixins/AWSHandlers.js'
// if (process.env.NODE_ENV !== 'production') require('dotenv').config()

export default {

  data() {
    return {
      form: {
        words: ''
      },
      submitStatus: 'PENDING',
      page: {
        title: 'Soke',
        subtitle: 'Type a word!',
        items: []
      }
    }
  },
  computed: {
    awsHandlers: function () {
      return new AWSHandlers(this)
    },
    awsSoke: function () {
      return JSON.parse(process.env.AWSSOKE)
    },
    awsSokeGetURL: function () {
      return this.awsSoke.get()
    }
  },
  methods: {
    feedBack: function (msg) {
      this.page.subtitle = msg
    },
    wordMe: function () {
      this.form.words = 'dog '
    },
    onSubmit: function () {
      this.awsHandlers.awsGET(this.awsSoke)
        .then((response) => {
          if (response.status === 200) {
            this.addItem(response.data)
            this.feedBack('Type another!')
          } else {
            this.feedBack('Something unexpected happened!')
            // this.addItem('something unexpected happened!')
          }
        })
        .catch((err) => {
          alert('err: ' + err)
        })
    },
    addItem: function (item) {
      // item {'name': ''}
      const id = this.page.items.length + 1
      this.page.items.push({ id: id, value: item })
    }
  }
}
</script>

<style scoped>
.band {
  width: 100%;
}

</style>
