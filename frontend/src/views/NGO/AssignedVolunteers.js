import React, { useEffect, useState } from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Grid, 
  Avatar, 
  Chip,
  CircularProgress,
  Button,
  Alert
} from '@mui/material';
import { VolunteerActivism } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { getVolunteers } from '../../models/VolunteerModel';
import { fetchVolunteers } from '../../services/api';

export default function AssignedVolunteers() {
  const [volunteers, setVolunteers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
  const loadVolunteers = async () => {
    try {
      const data = await getVolunteers();
      console.log('Voluntários recebidos:', data); // <-- VERIFIQUE ISSO NO CONSOLE
      setVolunteers(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
  loadVolunteers();
}, []);

  if (isLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: 40 }}>
        <CircularProgress size={60} />
      </div>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ margin: 2 }}>
        Erro ao carregar voluntários: {error}
      </Alert>
    );
  }

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom sx={{ color: 'primary.main' }}>
        <VolunteerActivism sx={{ mr: 1, verticalAlign: 'middle' }} />
        Voluntários Associados ({volunteers.length})
      </Typography>

      <Grid container spacing={3}>
        {volunteers.map((volunteer) => (
          <Grid item xs={12} md={6} key={volunteer.id}>
            <Card sx={{ 
              borderLeft: '4px solid', 
              borderColor: volunteer.status === 'approved' ? 'success.main' : 'warning.main',
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-3px)'
              }
            }}>
              <CardContent>
                <Grid container alignItems="center" spacing={2}>
                  <Grid item>
                    <Avatar sx={{ 
                      bgcolor: volunteer.status === 'approved' ? 'success.light' : 'warning.light',
                      color: 'white'
                    }}>
                      {volunteer.name?.[0] || '?'}
                    </Avatar>
                  </Grid>
                  <Grid item xs>
                    <Typography variant="h6">{volunteer.name || 'Sem nome'}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {volunteer.address || 'Sem endereço'}
                    </Typography>
                    <div style={{ marginTop: 8 }}>
                      {(volunteer.skills || []).slice(0, 3).map((skill) => (
                        <Chip 
                          key={skill}
                          label={skill}
                          size="small"
                          sx={{ mr: 1, mt: 1 }}
                          color="primary"
                        />
                      ))}
                    </div>
                  </Grid>
                  <Grid item>
                    <Button 
                      variant="contained"
                      color="secondary"
                      component={Link}
                      to={`/ngo/volunteer/${volunteer.id}`}
                      size="small"
                    >
                      Ver Detalhes
                    </Button>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {volunteers.length === 0 && (
        <Alert severity="info" sx={{ mt: 4 }}>
          Nenhum voluntário encontrado.
        </Alert>
      )}
    </div>
  );
}
