import TextField from "@mui/material/TextField";
import { useSelector } from "react-redux";
import { getResults } from "../../redux/resultsRedux";

function Results() {
	const results = useSelector(getResults);

	return (
		<div>
			<h2>Wyniki</h2>

			<h3>{ results.title }</h3>
      <p>{ results.task }</p>
      <TextField id="outlined-multiline-flexible" label="Testy jednostkowe" multiline size="small" margin="normal" fullWidth value={ results.unit_tests }  />
      <TextField id="outlined-multiline-flexible" label="Wzorcowe rozwiązanie" multiline size="small" margin="normal" fullWidth value={ results.solution }  />
		</div>
	);
}

export default Results;