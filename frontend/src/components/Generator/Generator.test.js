import { render } from '@testing-library/react';
import Generator from './Generator';

describe('Component Generator', () => {
	it('should render without crashing', () => {
		render(<Generator />);
	});
});