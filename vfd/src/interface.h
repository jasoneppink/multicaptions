#define DIRECTION(X,D)  if (D) (*(&X##_PORT - 1) |= (1<<X##_PIN)); else (*(&X##_PORT - 1) &= ~(1<<X##_PIN))
#define RAISE(X)    X##_PORT |= (1<<X##_PIN)
#define LOWER(X)    X##_PORT &= ~(1<<X##_PIN)
#define CHECK(X)    (*(&X##_PORT - 2) & (1<<X##_PIN))
#define SETPIN(X,V)  if (V) RAISE(X); else LOWER(X)

void initPort();
void writePort(uint8_t data);
