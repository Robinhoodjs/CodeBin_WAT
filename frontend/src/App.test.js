import { render } from '@testing-library/react';
import App from './App';

describe('Component App', () => {
  it('should render without crashing', () => {
    render(<App />);
  });
});
