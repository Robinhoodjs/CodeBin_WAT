import { render } from '@testing-library/react';
import Logo from './Logo';

describe('Component Logo', () => {
  it('should render without crashing', () => {
    render(<Logo />);
  });
});