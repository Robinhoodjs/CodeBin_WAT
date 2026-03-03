//selectors
export const getParameters = state => state.parameters;

// actions
const createActionName = actionName => `app/parameters/${actionName}`;
const UPDATE_TITLE = createActionName('UPDATE_TITLE');
const UPDATE_DIFFICULTY = createActionName('UPDATE_DIFFICULTY');
const UPDATE_DESCRIPTION = createActionName('UPDATE_DESCRIPTION');

// action creators
export const updateTitle = payload => ({ type: UPDATE_TITLE, payload });
export const updateDifficulty = payload => ({ type: UPDATE_DIFFICULTY, payload });
export const updateDescription = payload => ({ type: UPDATE_DESCRIPTION, payload });

const parametersReducer = (statePart = {}, action) => {
    switch(action.type) {
      case UPDATE_TITLE:
        return {...statePart, title: action.payload};
      case UPDATE_DIFFICULTY:
        return {...statePart, difficulty: action.payload};
      case UPDATE_DESCRIPTION:
        return {...statePart, description: action.payload};
      default:
        return statePart;
    }
  }

  export default parametersReducer;