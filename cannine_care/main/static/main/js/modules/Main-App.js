class MainApp {
  constructor() {}

  async mainApp() {
    
    if(document.getElementById("binhi-main-container")){
      Vue.createApp({
        delimiters: ['[[', ']]'],
        data(){
          return {
            message: "Hello World",
          }
        },
        components: {
  
        },
        async created(){

        },
        mounted(){
          console.log(this.message);
        },
        methods: {
        }
      }).mount("#binhi-main-container");
    }
  }
}

export { MainApp }; 