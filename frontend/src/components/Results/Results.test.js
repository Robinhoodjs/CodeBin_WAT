import { render } from '@testing-library/react';
import Results from './Results';

describe('Component Results', () => {
	it('should render without crashing', () => {
		render(<Results />);
	});
});