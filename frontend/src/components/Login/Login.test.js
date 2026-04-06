import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from './Login';

test('renderuje ekran logowania i weryfikuje główny nagłówek', () => {
    // BrowserRouter jest wymagany dla hooka useNavigate()
    render(
        <BrowserRouter>
            <Login />
        </BrowserRouter>
    );
    
    const headerElement = screen.getByText(/Witaj ponownie/i);
    expect(headerElement).toBeInTheDocument();
});