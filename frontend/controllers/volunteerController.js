const express = require('express');
const router = express.Router();
const axios = require('axios');

function authHeader(req) {
  return { Authorization: `Bearer ${req.session.token}` };
}

// List feed
router.get('/opportunities', async (req, res) => {
  const q = req.query.q || '';
  try {
    const resp = await axios.get('http://backend:8000/volunteer/opportunities', { headers: authHeader(req), params: { q } });
    res.render('volunteer/opportunities', { opportunities: resp.data, q });
  } catch {
    res.render('volunteer/opportunities', { opportunities: [], q, error: 'Erro ao carregar' });
  }
});

// Details
router.get('/opportunities/:id', async (req, res) => {
  try {
    const resp = await axios.get(`http://backend:8000/volunteer/opportunities/${req.params.id}`, { headers: authHeader(req) });
    res.render('volunteer/opportunityDetail', { opportunity: resp.data, error: null });
  } catch {
    res.redirect('/volunteer/opportunities');
  }
});

// Apply
router.post('/opportunities/:id/apply', async (req, res) => {
  try {
    await axios.post(`http://backend:8000/volunteer/opportunities/${req.params.id}/apply`, {}, { headers: authHeader(req) });
    res.redirect(`/volunteer/opportunities/${req.params.id}`);
  } catch (err) {
    // refetch opportunity on error
    const resp = await axios.get(`http://backend:8000/volunteer/opportunities/${req.params.id}`, { headers: authHeader(req) });
    res.render('volunteer/opportunityDetail', { opportunity: resp.data, error: 'Falha ao aplicar' });
  }
});

// My applications
router.get('/applications', async (req, res) => {
  try {
    const resp = await axios.get('http://backend:8000/volunteer/applications', { headers: authHeader(req) });
    res.render('volunteer/applications', { applications: resp.data });
  } catch {
    res.render('volunteer/applications', { applications: [], error: 'Erro ao carregar' });
  }
});

// Accepted
router.get('/applications/accepted', async (req, res) => {
  try {
    const resp = await axios.get('http://backend:8000/volunteer/applications/accepted', { headers: authHeader(req) });
    res.render('volunteer/acceptedApplications', { applications: resp.data });
  } catch {
    res.render('volunteer/acceptedApplications', { applications: [], error: 'Erro ao carregar' });
  }
});

module.exports = router;
