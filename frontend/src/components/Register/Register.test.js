import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Register from './Register';

test('renderuje ekran rejestracji i weryfikuje główny nagłówek', () => {
    // BrowserRouter jest wymagany, ponieważ wewnątrz komponentu korzystamy z hooka useNavigate()
    render(
        <BrowserRouter>
            <Register />
        </BrowserRouter>
    );
    
    // Wyszukujemy nagłówek na wyrenderowanej stronie
    const headerElement = screen.getByText(/Dołącz do nas/i);
    
    // Oczekujemy, że element znajduje się w dokumencie HTML
    expect(headerElement).toBeInTheDocument();
});