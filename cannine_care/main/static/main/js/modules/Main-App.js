class MainApp {
  constructor() {}

  async mainApp() {
    
    if(document.getElementById("cannine-care-main-container")){
      Vue.createApp({
        delimiters: ['[[', ']]'],
        data(){
          return {
            username: "",
            sendMessageUrl: "", 
            carouselIndex: 0,
          }
        },
        components: {
  
        },
        async created(){

        },
        mounted(){
          this.sendMessageUrl = document.getElementById('send-message-var').value;

          let vueApp = this;
          $(document).ready(function() {
            vueApp.initializeListener('#user-input-message-form');            
          });
        },
        methods: {
          switchCarouselImg(action){
            if(action == 'next'){
              this.carouselIndex = this.carouselIndex === 2 ? 0 : this.carouselIndex + 1;
            }else if (action == 'prev'){
              this.carouselIndex = this.carouselIndex === 0 ? 2 : this.carouselIndex - 1;
            }
          },

          initializeListener(container){
            if (!$(container).length) return;

            if(container === '#user-input-message-form'){
              this.applyListenerToUserChat();
            }
          },
          applyListenerToUserChat(){
            let vueApp = this;
            $("#user-input-message-form").submit(function(e) {
              e.preventDefault();
              var user_input = $('#user-input').val();
              
              $.ajax({
                type: 'GET',
                url: vueApp.sendMessageUrl,
                data: { user_input: user_input },
                success: function(data) {
                  var response = data.response;
                  
                  let userMessage = '<div class="user-bubble-container"><div class="user-name">' + (vueApp.userMessage ? vueApp.userMessage : " Guest ") + '</div><div class="user-message">' + user_input + '</div></div>';     
                  let chatbotResponse = '<div class="chatbot-bubble-container"><div class="chatbot-name">Cannine Care</div><div class="chatbot-message">' + response + '</div></div>';
                  
                  $('.message-display-container').append(userMessage);
                  $('.message-display-container').append(chatbotResponse);
                  $('#user-input').val(''); 
      
                  const $container = $(".message-display-container");
                  $container.scrollTop($container[0].scrollHeight);
                }
              });
            });
          },
        }
      }).mount("#cannine-care-main-container");
    }
  }
}

export { MainApp }; 