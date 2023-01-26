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


    //test img upload
	import http from 'k6/http';
	import { sleep } from 'k6';
	const img = open(`/Users/yangsejin/Desktop/hey_apple/monitor/testImg/5.jpg`, 'b');
	export default function () {
        const data = {
            file: http.file(img, `5.jpg`),
        };
        
        const res = http.post('http://localhost:8000/api/v1/orders/tasks', data); //img upload

        sleep(2);

	}

    //test img upload random
    // import http from 'k6/http';
	// import { check } from 'k6';
	// import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';
	// let testImgSelecter = Math.floor(Math.random() * 10); //1~9 까지의 랜덤선택
	// const img1 = open('/path/to/image1.png', 'b');
	// const img2 = open('/path/to/image2.jpg', 'b');
    // const txt = open('/path/to/text.txt');

	// 	export default function () {
    //         const fd = new FormData();
    //         fd.append('someTextField', 'someValue');
    //         fd.append('anotherTextField', 'anotherValue');
    //         fd.append('images', http.file(img1, 'image1.png', 'image/png'));
    //         fd.append('images', http.file(img2, 'image2.jpg', 'image/jpeg'));
    //         fd.append('text', http.file(txt, 'text.txt', 'text/plain'));

    //         const res = http.post('https://httpbin.test.k6.io/post', fd.body(), {
    //                 headers: { 'Content-Type': 'multipart/form-data; boundary=' + fd.boundary },
    //             });
    //         check(res, {
    //         'is status 200': (r) => r.status === 200,
    //             });
	// }