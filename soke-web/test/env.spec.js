import { mount } from '@vue/test-utils'
require ('dotenv').config()
// import Logo from '@/components/Logo.vue'

describe('.Env', () => {
  test('are env var initialied', () => {

    expect(process.env.DEVSITE).not.toBe(undefined)
  })

  test('is AWSSOKE initialied', () => {

    expect(process.env.AWSSOKE).not.toBe(undefined)
  })


  test('is NODE_ENV initialied', () => {

    expect(process.env.NODE_ENV).not.toBe(undefined)
  })
})