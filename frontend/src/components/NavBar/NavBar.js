import Grid from '@mui/material/Grid';
import Logo from '../Logo/Logo';
import NavTabs from '../NavTabs/NavTabs';
import styles from './NavBar.module.scss';

function NavBar() {
	return (
		<nav className={styles.nav}>
				<Grid container spacing={2}>
					<Grid size={3}>
						<Logo>CodeBin</Logo>
					</Grid>
					<Grid size={9}>
						<NavTabs />
					</Grid>
				</Grid>
		</nav >
	);
}

export default NavBar;