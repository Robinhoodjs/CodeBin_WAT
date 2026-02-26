import TextField from '@mui/material/TextField';
import Slider from '@mui/material/Slider';
import Button from '@mui/material/Button';
import { useState } from 'react';
import axios from 'axios';
import { useDispatch } from 'react-redux';
import { updateResults } from '../../redux/resultsRedux';
import styles from './Parameters.module.scss';

const marks = [
  {
    value: 0,
    label: 'łatwy',
  },
  {
    value: 50,
    label: 'średni',
  },
  {
    value: 100,
    label: 'trudny',
  },
];

function Parameters() {
  const [title, setTitle] = useState();
  const [description, setDescription] = useState();
  const [difficulty, setDifficulty] = useState();
  const [loading, setLoading] = useState(false);

  const dispatch = useDispatch();

  const convertDifficulty = difficulty => {
    if (difficulty == 0) {
      return 'latwy';
    } else if (difficulty == 50) {
      return 'sredni';
    } else {
      return 'trudny';
    }
  }

  const handleClick = async (event) => {
    setLoading(true);
    event.preventDefault(); // zapobiega odświeżeniu strony

    const payload = { // parametry do wysyłania
      title: title,
      description: description,
      difficulty: difficulty,
    };

    try {
      // I. Wysłanie POST
      const postResponse = await axios.post(
        'http://localhost:3131/api/parameters',
        payload,
        { headers: { 'Content-Type': 'application/json' } }
      );
      console.log('POST response:', postResponse.data);

      // II. Pobranie wyników GET
      const getResponse = await axios.get('http://localhost:3131/api/results/1');
      console.log('GET response:', getResponse.data);

      // Aktualizacja Redux
      dispatch(updateResults(getResponse.data));
      setLoading(false);

    } catch (error) {
      // Obsługa błędów zarówno POST jak i GET
      if (error.response) {
        // Serwer zwrócił status != 2xx
        console.error('Server error:', error.response.status, error.response.data);
      } else if (error.request) {
        // Brak odpowiedzi od serwera
        console.error('No response received:', error.request);
      } else {
        // Inny błąd w konfiguracji
        console.error('Error:', error.message);
      }
    }
  };

  return (
    <form autoComplete='on' onSubmit={ handleClick }>
      <h2>Parametry</h2>

      <TextField id="outlined-basic" label="Tytuł" variant="outlined" size="small" margin="normal" fullWidth onChange={(event) => setTitle(event.target.value)} />
      <TextField id="outlined-multiline-flexible" label="Opis" multiline rows={4} size="small" margin="normal" fullWidth onChange={(event) => setDescription(event.target.value)} />
      <p>Poziom trudności:</p>
      <Slider className={styles.slider} aria-label="Custom marks" defaultValue={0} step={50} marks={marks} onChange={(event) => setDifficulty(convertDifficulty(event.target.value))} />
      <Button type="submit" variant="contained" loading={loading}>Generuj</Button>
    </form>
  );
}

export default Parameters;