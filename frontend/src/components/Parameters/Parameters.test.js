import { render } from '@testing-library/react';
import Parameters from './Parameters';

describe('Component Parameters', () => {
	it('should render without crashing', () => {
		render(<Parameters />);
	});
});