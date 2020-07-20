<script>
//some default pre init
var PB = PB || {};PB.q = PB.q || [];PB.events = PB.events || [];

//PushBots ApplicationId (required)
PB.app_id = "5f087362afdf3934ac7142e5";
//Your domain name, must be HTTPS or localhost  (required)
PB.domain = "https://www.presimax.online";
//Update and uncomment it if you are using custom safari certificate for your app
PB.safari_push_id = "web.com.pushbots.safaripush";
//****************************************

PB.logging_enabled = true;
PB.auto_subscribe = true;

//Custom worker and manifest URL
//PB.worker_url = PB.domain + "/pushbots-worker.js";

//Welcome notification message
PB.welcome = {title:"Welcome ",message:"Thanks for subscribing!", url :PB.domain};

function sendNotification(){
      PB.register();
      PB.q.push(["sendNotification", {title:"Hey ",message:"Why not?", url :"https://www.presimax.online"}]);
}

</script>

<script src="//cdn.pushbots.com/js/sdk.min.js" type="text/javascript" onload="PB.init()" async></script>

