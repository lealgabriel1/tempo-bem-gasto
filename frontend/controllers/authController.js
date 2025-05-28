const express = require('express');
const router = express.Router();
const axios = require('axios');

// Render login/signup
router.get('/auth', (req, res) => res.render('auth/auth', { error: null }));

// Login
router.post('/login', async (req, res) => {
  const { username, password } = req.body;
  try {
    const resp = await axios.post(
      'http://backend:8000/auth/token',
      new URLSearchParams({ username, password }),
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    req.session.token = resp.data.access_token;
    if (resp.data.is_ngo) {
      res.redirect('/ngo/profile');
    } else {
      res.redirect('/volunteer/opportunities');
    }
  } catch {
    res.render('auth/auth', { error: 'Credenciais inválidas' });
  }
});

// Signup
router.post('/signup', async (req, res) => {
const { username, password, is_ngo } = req.body;
  try {
    // Converte para booleano e envia ao backend
    await axios.post('http://backend:8000/auth/signup', {
      username,
      password,
      is_ngo: is_ngo === 'true'
    });
    // Redireciona de volta ao login
    res.redirect('/auth');
  } catch (err) {
    // Mostra a mensagem de erro retornada pelo backend se houver
    const msg = err.response?.data?.detail || 'Falha no cadastro';
    res.render('auth/auth', { error: msg });
  }
});

module.exports = router;
