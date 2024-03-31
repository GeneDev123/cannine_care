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
            trainAIUrl: "",
            isLoading: false,

            accuracy: "",
            precision: "",
            recall: "",
            f1Score: "",
            confusionMat: "",

          }
        },
        components: {
  
        },
        async created(){

        },
        mounted(){
          this.sendMessageUrl = document.getElementById('send-message-var') ? document.getElementById('send-message-var').value : '';
          this.trainAIUrl = document.getElementById('train-ai-url') ? document.getElementById('train-ai-url').value : '';

          let vueApp = this;
          $(document).ready(function() {
            vueApp.initializeListener('#user-input-message-form');       
            vueApp.initializeListener('#profile-page-container')
            vueApp.initializeTrainBtn();     
          });
        },
        methods: {
          initializeTrainBtn(){
            let vueApp = this;
            $(document).ready(function() {
              $('#train-ai-btn').on('click', function() {
                vueApp.isLoading = true;
                $.ajax({
                  url: vueApp.trainAIUrl,
                  type: 'GET',
                  success: function(response) {
                    
                    setTimeout(function() {
                      alert('Notice: Model Successfully Trained');
                      vueApp.isLoading = false;
                      console.log(response.model_output);
                      vueApp.accuracy = response.model_output.accuracy;
                      vueApp.precision = response.model_output.precision;
                      vueApp.recall = response.model_output.recall;
                      vueApp.f1Score = response.model_output.f1Score;
                      vueApp.confusionMat = response.model_output.confusion_mat;
                      console.log(response.model_output);
                    }, 2000);
                  },
                  error: function(error) {
                    alert('Notice: Model Training failed');
                    vueApp.isLoading = false;
                  }
                });
              });
            });
          },
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
            else if(container == "#profile-page-container"){
           
              var readonlyCheckeboxes = document.querySelectorAll('.readonly-checkboxes');
              var readonlyInputs = document.querySelectorAll('.readonly-inputs');

              readonlyCheckeboxes.forEach(function(checkbox) {
                checkbox.addEventListener('click', function(event) {
                  event.preventDefault();
                  checkbox.checked = !checkbox.checked;
                  return false;
                });
              });

              readonlyInputs.forEach(function(input) {
                input.readOnly = true;
                input.addEventListener('click', function(event) {
                  event.preventDefault();
                });
              });
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