// import axios from 'axios'
// import { DFRequestPost } from './DFRequestPost.js'
// import { DFRequestGet } from './DFRequestGet.js'
// import { DFRequestPut } from './DFRequestPut.js'
// import { DFHeader } from './DFHeader.js'
class AWSHandlers {
  /*
  consistant interface with Amazon Web Services
  */
  constructor(component) {
    // this.header = dfSession;
    // this.session = dfSession;
    // this.dfSystem = dfSystem;
    this.component = component
  }

  async awsGET(awsService) {
    /*
      awsService is {"get":"https://{rest-api-id}.execute-api.{aws-region}.amazonaws.com/{aws-stage-name}/{aws-api-name}"}
    */

    const response = await this.component.$axios(awsService.get)

    return response
  }
}

export { AWSHandlers }
