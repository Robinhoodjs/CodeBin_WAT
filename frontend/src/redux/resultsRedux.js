//selectors
export const getResults = state => state.results;

// actions
const createActionName = actionName => `app/results/${actionName}`;
const UPDATE_RESULTS = createActionName('UPDATE_RESULTS');

// action creators
export const updateResults = payload => ({ type: UPDATE_RESULTS, payload });

const resultsReducer = (statePart = {}, action) => {
    switch(action.type) {
      case UPDATE_RESULTS:
        return action.payload;
      default:
        return statePart;
    }
  }

  export default resultsReducer;