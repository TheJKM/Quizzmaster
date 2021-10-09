import $ from 'dom7';
import Framework7 from 'framework7/bundle';

// Import F7 Styles
import 'framework7/framework7-bundle.css';

// Import Icons and App Custom Styles
import '../css/icons.css';
import '../css/app.css';


// Import Routes
import routes from './routes.js';

// Import main app component
import App from '../app.f7.html';

import my from './my.js';

my.app = new Framework7({
  name: 'Quizzmaster',
  theme: 'aurora',
  el: '#app',
  component: App,
  routes: routes,
  autoDarkTheme: true,
  on: {
    init: function() {
      let mainView = this.views.create(".view-main", {
        url: "/",
        browserHistory: true,
        browserHistorySeparator: "#"
      });
    },
  },
});
