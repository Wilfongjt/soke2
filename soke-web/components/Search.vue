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
        <div>{{ item.value }}</div>
        <span>&nbsp;</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { AWSHandlers } from './mixins/AWSHandlers.js'
// if (process.env.NODE_ENV !== 'production') require('dotenv').config()
/* eslint-disable no-console */
// console.log('search: ' + process.env.DEVSITE)
/* eslint-enable no-console */
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
    awsGatewayParameters: function () {
      return 'keywords=%s'.replace('%s', this.form.words)
    },
    awsGateway: function () {
      /*
      * Returns JSON object holding URLs for webservice {get: "", post: "", ...}
      */
      let val = {}
      try {
        // get the gateway url
        val = JSON.parse(process.env.AWSSOKE)
      } catch (err) {
        /* eslint-disable no-console */
        console.log('awsGateway error: ' + err)
        /* eslint-enable no-console */
        val = {}
      }
      return val
    }
  },
  methods: {
    feedBack: function (msg) {
      this.page.subtitle = msg
    },
    wordMe: function () {
      this.form.words = 'dog '
    },
    onSubmit: function () { // submit button
      // put together url to get items
      const awsGatewayURLWithParameters = '%s?%p'
        .replace('%s', this.awsGateway.get)
        .replace('%p', this.awsGatewayParameters)
      // clear the list
      this.page.items = []
      // make the call
      this.awsHandlers.awsGET(awsGatewayURLWithParameters)
        .then((response) => {
          if (response.status === 200) {
            // this.addItem(response.data)
            /* eslint-disable no-console */
            let i = 0
            for (i = 0; i < response.data.results.length; i++) {
              this.addItems(response.data.results[i].Items)
            }
            /* eslint-enable no-console */
            this.feedBack('Type another!')
          } else {
            this.feedBack('Something unexpected happened!')
            // this.addItem('something unexpected happened!')
          }
        })
        .catch((err) => {
          /* eslint-disable no-console */
          console.log('submit error: ' + err)
          /* eslint-enable no-console */
        })
    },
    addItem: function (item) {
      // show result item to user
      const id = this.page.items.length + 1
      this.page.items.push({ id: id, value: item.data })
    },
    addItems: function (itemArray) {
      // break down result into managable chunks
      /* eslint-disable no-console */
      // console.log('results.results.Items: ' + JSON.stringify(results.results.Items))
      let i = 0
      for (i = 0; i < itemArray.length; i++) {
        this.addItem(itemArray[i])
      }
      /* eslint-enable no-console */
    }

  }
}
</script>

<style scoped>
.band {
  width: 100%;
}

</style>
