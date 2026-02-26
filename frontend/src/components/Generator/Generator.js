import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Parameters from '../Parameters/Parameters';
import Results from '../Results/Results';
import styles from './Generator.module.scss';

function Generator() {
	return (
		<main className={styles.main}>
			<Container>
				<p>Witaj w generatorze zadań!</p>

				<Grid container spacing={2}>
        	<Grid size={6}>
        	  <Parameters />
       	 	</Grid>
       		<Grid size={6}>
          	<Results />
       	 	</Grid>
      	</Grid>
			</Container>
		</main>
	);
}

export default Generator;