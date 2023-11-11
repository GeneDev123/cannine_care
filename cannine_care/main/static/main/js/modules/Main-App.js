class MainApp {
  constructor() {}

  async mainApp() {
    
    if(document.getElementById("cannine-care-main-container")){
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
      }).mount("#cannine-care-main-container");
    }
  }
}

export { MainApp }; 