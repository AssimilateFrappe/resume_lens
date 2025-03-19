import './App.css'
import { FrappeProvider } from 'frappe-react-sdk'
import UploadjobDescription from './component/UploadJobDescription'

function App() {

  return (
	<div className="App">
	  <FrappeProvider>
		<UploadjobDescription/>
	  </FrappeProvider>
	</div>
  )
}

export default App
