//POST
// import http from 'k6/http';

// export default function () {
//   const url = 'http://';
//   const payload = JSON.stringify({
//     email: '1106q@naver.com',
//     password: 'bbb',
//   });

//   const params = {
//     headers: {
//       'Content-Type': 'application/json',
//     },
//   };

//   http.post(url, payload, params);
// }

//GET ..email TEST
// import http from 'k6/http';

// export default function () {
//     let email = "1106q@naver.com"
//     for (let id = 1; id <= 4; id++) {
//         http.get(`http://localhost:8000/api/v1/bills?email=${email}&orderpayment_id=${id}`);
//     }
// }

//GET ..fruit TEST
// import http from 'k6/http';

// export default function () {
//     for (let id = 1; id <= 4; id++) {
//         http.get(`http://localhost:8000/api/v1/fruits/${id}`);
//     }
// }

