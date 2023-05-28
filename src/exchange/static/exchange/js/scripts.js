var price_buy = 0;
var price_sell = 0;
let cryptocurrency = ['BTC', 'ETH'];
let stable_coin = ['USDT', 'BUSD'];

window.onload = function()
{
    updateBankOptions();
}

function clearInputFields() {
    const moneyGiveInput = document.getElementById('id_money_give');
    const moneyTakeInput = document.getElementById('id_money_take');
    document.getElementById('go_to_form').disabled = true;
    moneyGiveInput.value = "";
    moneyTakeInput.value = "";
}
function request(get, take) {
    stab = ['USD', 'EUR', 'USDT', 'BTC', 'ETH']
    table_get = ['RUB', 'BYN', 'USD', 'EUR', 'USDT', 'BTC', 'ETH']
    table_get_take = ['UAH']
    table_take = ['UAH']
    table_take_get = table_get
    if (get === take || get === 'PM' && take !== 'UAH' || take === 'PM' && get !== 'UAH'){
        return;
    }

    if (table_get.includes(get) && table_get_take.includes(take)){
        const table = document.getElementById("get").firstElementChild;
        for (let row of table.rows) {
          const cell1 = row.cells[0];
          if (cell1.innerText === get + '/' + take) {
            const cell2 = row.cells[1];
            const Rate = parseFloat(cell2.innerText);
            price_buy = Rate;

            console.log(price_buy);
            return;
          }
        }
    }else if (table_take.includes(get) && table_take_get.includes(take)){
        const table = document.getElementById("take").firstElementChild;
        for (let row of table.rows) {
          const cell1 = row.cells[0];
          if (cell1.innerText === get + '/' + take) {
            const cell2 = row.cells[1];
            const Rate = parseFloat(cell2.innerText);
            if (stab.includes(take)){
                price_buy = 1 / Rate;
            } else{
                price_buy = Rate;
            }

            console.log(price_buy);
            return;
          }
        }
    }else if (get === 'PM' && take === 'UAH') {
        console.log(take)
        const table = document.getElementById("get_pm").firstElementChild;
        const Rate = table.querySelectorAll('th');
        const secondTh = Rate[1];
        price_buy = parseFloat(secondTh.textContent);

        console.log(price_buy)
        return
    }else if (take === 'PM' && get === 'UAH'){
        const table = document.getElementById("take_pm").firstElementChild;
        const Rate = table.querySelectorAll('th');
        const secondTh = Rate[1];
        price_buy = 1 / parseFloat(secondTh.textContent);

        console.log(price_buy);
        return;
    }else {
        const apiUrl = `/api/v1/exchangeRate/?get=${get}&take=${take}`;
        fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
          if (data.price) {
              price_buy = parseFloat(data.price);

              console.log(price_buy);
          }})
    }
}
