import Container from '@mui/material/Container';
import styles from './Home.module.scss';

function Home() {
	return (
		<main className={styles.main}>
			<Container>
				<p>Witaj na głównej stronie!</p>
			</Container>
		</main>
	);
}

export default Home;