const express = require('express');
const router = express.Router();
const axios = require('axios');

// Helper to get auth header
function authHeader(req) {
  return { Authorization: `Bearer ${req.session.token}` };
}

// NGO Profile form
router.get('/profile', async (req, res) => {
  res.render('ngo/profile', { error: null });
});

// Submit profile
router.post('/profile', async (req, res) => {
  try {
    const { name, description } = req.body;
    await axios.post('http://backend:8000/ngo/profile', { name, description }, { headers: authHeader(req) });
    res.redirect('/ngo/opportunities');
  } catch {
    res.render('ngo/profile', { error: 'Erro ao salvar perfil' });
  }
});

// List opportunities
router.get('/opportunities', async (req, res) => {
  try {
    const resp = await axios.get('http://backend:8000/ngo/opportunities', { headers: authHeader(req) });
    res.render('ngo/opportunities', { opportunities: resp.data });
  } catch {
    res.render('ngo/opportunities', { opportunities: [], error: 'Não foi possível carregar' });
  }
});

// View candidates for an opportunity
router.get('/opportunities/:id/candidates', async (req, res) => {
  try {
    const resp = await axios.get(`http://backend:8000/ngo/opportunities/${req.params.id}/candidates`, { headers: authHeader(req) });
    res.render('ngo/candidates', { candidates: resp.data, oppId: req.params.id });
  } catch {
    res.redirect('/ngo/opportunities');
  }
});

// Approve/reject candidate
router.post('/opportunities/:oppId/candidates/:appId', async (req, res) => {
  const { status } = req.body;
  try {
    await axios.post(
      `http://backend:8000/ngo/opportunities/${req.params.oppId}/candidates/${req.params.appId}`,
      { status },
      { headers: authHeader(req) }
    );
    res.redirect(`/ngo/opportunities/${req.params.oppId}/candidates`);
  } catch {
    res.redirect(`/ngo/opportunities/${req.params.oppId}/candidates`);
  }
});

module.exports = router;
