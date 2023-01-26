/* ordering customer's last name alphabetically */
SELECT First_name, Last_name FROM Customer ORDER BY Last_name ASC;


/* highest total price of a bill*/
SELECT ID, Total_price, MAX(Total_price) FROM Bill;

/* the customer who has the highest balance */
SELECT c.First_name, c.Last_name, w.MAX(Balance) FROM wallet w, Customer c, Profile p
     WHERE p.Username = w.Profile_Username and p.Customer_ID = c.ID;

/* تامین کننده هایی که در یک شهر هستند */
SELECT distinct p1.Name, p1.ID, p2.Name, p2.ID FROM Provider p1, Provider p2
     WHERE p1.City = p2.City;

/* سه کاربر برتر ماه */
SELECT c.First_name, c.Last_name FROM Bill b, Customer c
     WHERE b.Date between '2021-03-01' and '2021-03-31' and c.ID = b.Cart_Customer_ID
     GROUP BY b.Cart_Customer_ID
     ORDER BY sum(Total_price) DESC LIMIT 3; 

/*اِن سفارش آخر هر کاربر مشخض (با گرفتن آیدی کاربر)*/
SELECT p.Name, b.Cart_Customer_ID FROM Product p, Bill b, Cart_contains_Product ccp
     WHERE p.ID = ccp.Product_ID and ccp.Cart_ID = b.Cart_ID and b.Cart_Customer_ID = 1
     ORDER BY b.Date DESC LIMIT 2;