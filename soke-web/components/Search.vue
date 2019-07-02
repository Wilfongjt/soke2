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
    <!--ul id="search-results"-->
      <div v-for="item in page.items" :key="item.id">
        <span>&nbsp;</span>
        <p class="subtitle">
          {{ item.title }}
        </p>
        <p>
          <span v-html="item.description"></span>
        </p>
      </div>
    <!--/ul-->
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
    wordList: function () {
      return this.form.words.split(' ')
    },
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
        this.log('awsGateway error: ' + err)
        val = {}
      }
      return val
    }
  },
  methods: {
    log: function (msg) {
      /* eslint-disable no-console */
      console.log(msg)
      /* eslint-enable no-console */
    },
    feedBack: function (msg) {
      this.page.subtitle = msg
    },
    wordMe: function () {
      this.form.words = 'dog '
    },
    highlight: function (description) {
      let desc = description
      let i = 0
      for (i in this.wordList) {
        desc = desc.replace(
          this.wordList[i] + ' ',
          '<strong>%s</strong>'.replace('%s', this.wordList[i] + ' ')
        )
      }
      return desc
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
            let i = 0
            for (i = 0; i < response.data.results.length; i++) {
              this.addItems(response.data.results[i].Items)
            }
            this.feedBack('Type another!')
          } else {
            this.feedBack('Something unexpected happened!')
            // this.addItem('something unexpected happened!')
          }
        })
        .catch((err) => {
          this.log('submit error: ' + err)
        })
    },
    addItem: function (item) {
      // show result item to user
      const id = this.page.items.length + 1
      this.page.items.push({
        id: id,
        title: item.title,
        description: this.highlight(item.data)
      })
    },
    addItems: function (itemArray) {
      // break down result into managable chunks
      // console.log('results.results.Items: ' + JSON.stringify(results.results.Items))
      let i = 0
      for (i = 0; i < itemArray.length; i++) {
        this.addItem(itemArray[i])
      }
    }
  }
}
</script>

<style scoped>
.band {
  width: 100%;
}

</style>
