import { render } from '@testing-library/react';
import NavBar from './NavBar';

describe('Component NavBar', () => {
  it('should render without crashing', () => {
    render(<NavBar />);
  });
});