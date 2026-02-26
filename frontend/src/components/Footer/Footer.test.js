import { render } from '@testing-library/react';
import Footer from './Footer';

describe('Component Footer', () => {
	it('should render without crashing', () => {
		render(<Footer />);
	});
});