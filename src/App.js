import { Fragment } from "react"; // thẻ ảo k chứa j
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { publicRouters, privateRouters } from "./router";
import Layoutmaster from "./components/Layoutmaster";
import Login from "./components/login/Login";
import Demo2 from "./components/demo2";
import Cookies from "js-cookie";
import "react-tabs/style/react-tabs.css";
import "react-datepicker/dist/react-datepicker.css";
let token = Cookies.get("user");

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/demo2" element={<Demo2 />}></Route>
          {token
            ? privateRouters.map((route, index) => {
                const Page = route.component;
                let Layout = Layoutmaster;

                if (route.layout) {
                  Layout = route.layout;
                } else if (route.layout === null) {
                  Layout = Fragment;
                }

                return (
                  <Route
                    key={index}
                    path={route.path}
                    element={
                      <Layout>
                        <Page />
                      </Layout>
                    }
                  />
                );
              })
            : publicRouters.map((route, index) => {
                const Page = route.component;

                return (
                  <Route key={index} path={route.path} element={<Page />} />
                );
              })}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
