import { render } from '@testing-library/react';
import NavTabs from './NavTabs';

describe('Component NavTabs', () => {
	it('should render without crashing', () => {
		render(<NavTabs />);
	});
});