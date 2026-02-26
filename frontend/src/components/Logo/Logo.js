import { Link } from 'react-router-dom';
import RocketLaunch from '@mui/icons-material/RocketLaunch';
import styles from './Logo.module.scss';

function Logo(props) {
	return (
		<Link className={styles.logo} to='/'><RocketLaunch className={styles.icon} />{props.children}</Link>
	);
}

export default Logo;