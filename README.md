# Solutions to the practical assignment: "Implementing a 'baby' blockchain"

Distributed Lab Course in Summer of 2022.

## Description

The main purpose of this project is to understand the basic workings of blockchain technology. 
Awareness is gained by implementing your own minimal version of blockchain 
(no decentralisation and consensus mechanisms, just basic structures).


## Overview and purpose of the system/product

The system I wanted to develop is one where users can buy something in an auction format and also, in the future, the possibility of scalability, including: the added functionality of data exchange systems, exchanges, registries and those or other systems that can improve the project.
The system will be used for the creation and/or purchase of digital products such as novels, books, artworks and any other items not requiring a lot of storage space, ideally up to 10 Mb.

## Content of the system (system boundaries)

The main components of the system will be as follows:
* Hash: a "wrapper" class for the use of the gash function;
* Signature: a "wrapper" class to use a digital signature;
* KeyPair: a class designed to work with keys;
* Account: a class for working with the wallet, creating transactions and signing data;
* Operation: a class allowing to create a payment operation;
* Transaction: a class allowing to create a transaction containing payments of users;
* Block: a class that forms a block with transactions;
* Blockchain: a class to create a blockchain, a database of coins and existing transactions;
* DigitalProduct: a class that describes the content and/or content of a digital product.



## Interaction (potential) of the product (with other products and components)

The system itself will need visualization and functionality such as, exhibition, product discussion, notification of auction start and so on.
Also, if the system is to be scaled up, the use of the functionality of data exchange systems, registries, voting platforms, if useful.


## Product functions (brief description)

1. Ability to create and/or purchase a digital product.
 2. Ability to view the main features of the product.
 3. The ability to verify who owns the product in question.
 4. The ability to ensure the anonymity of the buyer and trade for the consumer.
In my opinion, this is the basic functionality needed for an auction of digital products, ready to suggests.

## Security requirements

At the moment it is rather difficult for me to understand what the security requirements are; so, if possible, please suggest what is meant by security requirements.
Is it stability of function or the same anonymity, integrity of the system?

## User characteristics (who is the end user of the system)

Authors, translators, readers, fans and so on. All people who want to own, create, use, sell, are able to use this product, to ensure all these points; while providing their anonymity and the ability to verify ownership of this or that product.

## Limitations

The most important issue is the resource cost, i.e. the memory and speed of the auction itself.
At the 1st stage I plan to limit the size of the block to 10 megabytes, respectively, the maximum amount of the transaction will be 25 percent of this value.
I plan to use FBA algorithm to achieve consensus.

---

`Ready to hear opinions and suggestions on this idea.
Ready for criticism.
Thanks for your feedback!`


# `Temporary' Ukrainian version of the text above (If my English, so bad :(  )

## Огляд та призначення системи продукту
Мені хотілося розробити систему, за допомогою якої користувачі зможуть щось придбати у форматі аукціону, а також, у майбутньому, можливість, масштабування, включаючи: добавлені функціоналу систем обміну даних, бірж, реєстрів, та тих чи інших систем, які зможуть покращити проект.
Система буде призначена для створення та/або придбання цифрового продукту, до прикладу, новели, книжки, малюнки, та будь-яких інші речі що не потребують великого обсягу пам'яті, в ідеалі до 10 Mb.

## Зміст системи кордони системи
* Основні складові системи будуть такими:
* Hash: клас-“обгортка” для використання геш-функції.;
* Signature: клас-“обгортка” для використання цифрового підпису;
* KeyPair: клас, який призначено для роботи із ключами;
* Account: клас, який призначено для роботи із гаманцем, створення операцій та підпису даних;
* Operation:  клас, який дозволяє створити операцію платежу;
* Transaction: клас, який дозволяє створити транзакцію, що містить платежі користувачів;
* Block: клас, що формує блок із транзакціями;
* Blockchain: клас, що дозволяє створити ланцюжок блоків, базу даних монет та існуючих транзакцій;
* DigitalProduct: клас, який описує зміст та/або вміст цифрового продукту.

Взаємодія з іншими продуктами.
Сама собою система буде потребувати візуалізації та такого функціоналу як, виставка, обговорення продукту, сповіщення про початок аукціону і так далі.
Також, якщо система буде Розширюватися, то, якщо буде доцільно, впровадження функціоналу систем обміну даних, реєстрів, платформ для голосування.

Функції продукти.
 1. Можливість створити та/або купити цифровий продукт.
 2. Можливість переглянути основні характеристики продукту.
 3. Можливість перевірити, хто є власником даного продукту.
 4. Забезпечення анонімності покупця та продавцця за потребителем.
Як на мою думку, це є базовий функціонал, що потрібен для аукціону цифрових продуктів, готовий до пропозицій.

Вимоги до безпеки.
На даний момент мені достатньо складно зрозуміти, що є вимогами до безпеки; тому, якщо, є така можливість підкажіть, будь ласка, що мається на увазі під вимогами до безпеки.
Це стійкість функції чи та сама анонімність, цілісність системи?

Характеристики користувачів.
Автори, перекладачі, читачі, фанати і так далі. Всі люди що хочуть володіти, створювати, користуватися, продавати, мають можливість використовувати даний продукт, для забезпечення всіх цих пунктів; причому забезпечуючи свою анонімність та можливість перевірки на володіння тим чи іншим продуктом.

Обмеження.
Найбільш важливе питання це затратність ресурсів, тобто пам'яті та швидкості проведення самого аукціону.
На 1-му етапі планую вести обмеження до 10 мегабайт розміру блоку, відповідно Максимальний об’єм транзакції буде 25 відсотків від даного значення.
Планую використовувати алгоритми досягнення консенсусу FBA.
Готовий почути думки та пропозиції щодо даної ідеї.
Готовий до критики.
Дякую за увагу!

## Authors

ex. Kyrylo Riabov [Gmail](kyryl.ryabov@gmail.com)

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.

* [Bitcoin White paper](https://bitcoin.org/bitcoin.pdf)
* [Blockchain demo](https://andersbrownworth.com/blockchain/hash)


