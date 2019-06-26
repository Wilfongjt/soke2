
class AWSHandlers {
  /*
  consistant interface with Amazon Web Services
  */
  constructor(component) {
    // set the nuxt component
    this.component = component
  }

  async awsGET(awsGatewayURLWithParameters) {
    const response = await this.component.$axios(awsGatewayURLWithParameters)
    return response
  }
}

export { AWSHandlers }
