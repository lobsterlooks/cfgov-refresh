import { render } from 'react-dom';
import Greeting from './components/greeting';
import Counter from './components/counter';
import { configure as configureMobX } from 'mobx';

configureMobX({ enforceActions: 'observed' });

const App = () => (
  <div className="hello">
    <Greeting />
    <Counter />
  </div>
);

render(<App />, document.querySelector('#mmt-my-money-calendar'));
