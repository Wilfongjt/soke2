
class AWSHandlers {
  /*
  consistant interface with Amazon Web Services
  */
  constructor(component) {
    // set the nuxt component
    this.component = component
  }

  async awsGET(awsGatewayURLWithParameters, awsHeader) {
    const response = await this.component.$axios(awsGatewayURLWithParameters, { headers: awsHeader })
    return response
  }
}

export { AWSHandlers }
