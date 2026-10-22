let arr=['a','b','c','d','e'
]
console.log(arr.slice(0,5));
console.log(arr.slice(-2));
console.log(arr.slice(1,-3))
arr.forEach(arr=>{
    console.log(arr);
})
console.log(arr.slice())
console.log([...arr])
console.log(arr.splice(2));
console.log(arr);
console.log(arr.splice(-1));

console.log(arr);

 arr=['a','b','c','d','e'
]
console.log(arr.reverse());
let arr2=[1,2,3,4,5];
console.log(arr.concat(arr2));
console.log (arr2.join("-"));
let a1=[1,2,3]
console.log(a1[0]);
console.log(a1.at(0));
console.log(a1[a1.length-1]);
console.log(a1.slice(-1));
console.log(a1.at(-1));


console.log("tayyab".at(0));
const movements=[200,450,-400,3000,-650,-130,70,1300];
for (const movement of movements) {
if (movement>0) {
    console.log(`you have deposited
        ${movement}`);
    
}    else
{
    console.log(`you withdrew ${Math.abs((movement))}`);
}}
console.log(`forEach`);

movements.forEach(function (movement,i) {
    if (movement>0) {
        console.log(`you have deposited
            ${movement}which is at ${i}`);
        
    }    else
    {
        console.log(`you withdrew ${Math.abs((movement))} which is at ${i}`);
    } 
})