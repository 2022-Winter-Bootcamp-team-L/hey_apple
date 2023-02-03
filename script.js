import http from 'k6/http';
import { sleep } from 'k6';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';

export const options = {
    stages: [
        { duration: '30s' , target: 30},
        { duration: '20s' , target: 10},
        { duration: '10s' , target: 5},
    ],
};

//GET ..email TEST
// export default function () {
//     let email = "1106q@naver.com"
//         http.get(`http://svheyapple.com/api/v1/bills?email=${email}&orderpayment_id=20aa4bae-31d5-445d-ae31-21b44b87c9f6`);
// }

//GET ..elastic_serch TEST
// export default function () {
//         http.get(`http://svheyapple.com/heyapple/_search?q=name:Apple`);
// }
//GET ..result TEST
// export default function () {
//         http.get(`http://svheyapple.com/api/v1/orders/tasks/20aa4bae-31d5-445d-ae31-21b44b87c9f6`);
// }
//GET ..fruit TEST
// export default function () {
//         http.get(`http://svheyapple.com/api/v1/fruits/1`);
// }

//POST ..test img upload random
// let testImgSelecter = Math.floor(Math.random() * 10); //1~9 까지의 랜덤선택
// const img1 = open('monitor/testImg/5.jpg', 'b');

// 	export default function () {
//         const fd = new FormData();
//         fd.append('images', http.file(img1, '5.jpg', 'image/jpeg'));
//         const res = http.post('http://svheyapple.com/api/v1/orders/tasks', fd.body(), {
//                 headers: { 'Content-Type': 'multipart/form-data; boundary=' + fd.boundary },
//             });
//         check(res, {
//         'is status 200': (r) => r.status === 200,
//             });
// }

//random api start
let randomNumber = Math.floor(Math.random() * 4) + 1;
const img1 = open('monitor/testImg/5.jpg', 'b');
export default function () {
    sleep(1);
    switch (randomNumber) {
        case 1:
          console.log("elastic test");
          elastic_api ();
          break;
        case 2:
          console.log("fruit test");
          fruit_api ();
          break;
        case 3:
          console.log("email test");
          email_api ();
          break;
        case 4:
          console.log("upload_api");
          const fd = new FormData();
          fd.append('images', http.file(img1, '5.jpg', 'image/jpeg'));
          const res = http.post('http://svheyapple.com/api/v1/orders/tasks', fd.body(), {
                  headers: { 'Content-Type': 'multipart/form-data; boundary=' + fd.boundary },
              });
          check(res, {
          'is status 200': (r) => r.status === 200,
              });
          break;
        default:
          console.log("The number is not between 1 and 4");
          break;
      }   
}

function elastic_api (){
    http.get(`http://svheyapple.com/heyapple/_search?q=name:Apple`);
}

function fruit_api (){
    http.get(`http://svheyapple.com/api/v1/fruits/1`);
}
function email_api (){
    let email = "1106q@naver.com"
    http.get(`http://svheyapple.com/api/v1/bills?email=${email}&orderpayment_id=e9172f67-6a3e-4f41-8ed0-2ae3e80e1145`);
}
function upload_api (){
        const fd = new FormData();
        fd.append('images', http.file(img1, '5.jpg', 'image/jpeg'));
        const res = http.post('http://svheyapple.com/api/v1/orders/tasks', fd.body(), {
                headers: { 'Content-Type': 'multipart/form-data; boundary=' + fd.boundary },
            });
        check(res, {
        'is status 200': (r) => r.status === 200,
            });
}
//random api end