const express = require('express');
const exphbs = require('express-handlebars');
const session = require('express-session');
const path = require('path');

const authController = require('./controllers/authController');
const ngoController = require('./controllers/ngoController');
const volunteerController = require('./controllers/volunteerController');

const app = express();

// View engine setup
app.engine('hbs', exphbs({ extname: '.hbs', layoutsDir: 'views/layouts', defaultLayout: 'main' }));
app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.use(session({ secret: 'your-secret-key', resave: false, saveUninitialized: false }));

// Routes
app.use('/', authController);
app.use('/ngo', ngoController);
app.use('/volunteer', volunteerController);

app.listen(3000, () => console.log('Frontend running at http://localhost:3000'));
