import { MainApp } from './modules/Main-App.js'

(async function($) {

  let mainApp = new MainApp()
  let app = await mainApp.mainApp()
  
})(jQuery);