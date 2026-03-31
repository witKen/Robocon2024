void trans(byte data[], int datasize, int datareply, int mid) {
  byte reply[datareply];
  bool success = false;
  int count = 0;
  while (success == false) {
    serialM.write(data, datasize);
    delay(5);
    if (serialM.available() > 0) {
      serialM.readBytes(reply, datareply);
    }
        for (int i = 0; i < datareply; i++) {
          debug.print(reply[i], HEX);
          debug.print(" ");
        }
        debug.println();
        
    byte checksum = reply[0] + reply[1] + reply[2] + reply[3];
    if (reply[0] == 0x3e && reply[1] == 0xa2 && reply[2] == mid && reply[3] == 0x07 && reply[4] == checksum) {
      success = true;
    } else {
      success = false;
      count++;
    }
    if (count > 10) {
      break;
    }
  }
}

void run_speed(int mid, long velo) {
  byte speed[10] = { 0x3e, 0xa2, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
  long ratio = velo * 100 * 10;
  speed[9] = 0;
  speed[2] = mid;
  speed[4] = speed[0] + speed[1] + speed[2] + speed[3];
  for (int i = 5; i < 9; i++) {
    speed[i] = ratio >> (8 * (i - 5));
    speed[9] += speed[i];
  }
  trans(speed, 10, 13, mid);
}

void motorMotion(double _vx, double _vy, double _w, double _dis, double _ang, double _ta) {
  _dis += offset;
  _ang += offsetang;
  _w = radians(_w);
  _ang = radians(_ang);
  double _dxa, _dya;
  double _t = 0;
  double _ax = (_vx / _ta) ;
  double _ay = (_vy / _ta) ;
  double _aw = (_w / _ta);

  if (_vx != 0  || _vy != 0) {
    if (_ax != 0) {
      _dxa = sq(_vx) / (2 * _ax); // distance acceleration for 100ms
    } else {
      _dxa = 0;
    }
    if (_ay != 0) {
      _dya = sq(_vy) / (2 * _ay);
    } else {
      _dya = 0;
    }
    double _da = sqrt(sq(_dxa) + sq(_dya));
    double _d = _dis - (2 * _da);
    double _v = sqrt(sq(_vx) + sq(_vy));
    _t = abs(_d / _v);
  } else {
    double _anga = abs(sq(_w) / (2 * _aw));
    double _angl = _ang - (2 * _anga);
    _t = abs(_angl / _w);
  }
  long countTa = 0;
  long countTt = 0;
  double _vxx = 0;
  double _vyy = 0;
  double _ww = 0;

  double tmp = 0;
  while (countTa <= _ta * 1000) {
    long t1 = millis();
    _vxx += _ax * tmp / 1000;
    _vyy += _ay * tmp / 1000;
    _ww += _aw * tmp / 1000;

    w1 = degrees(((_vxx - _vyy) - (_ww * (lx + ly))) / r);
    w2 = degrees(((_vxx + _vyy) + (_ww * (lx + ly))) / r);
    w3 = degrees(((_vxx + _vyy) - (_ww * (lx + ly))) / r);
    w4 = degrees(((_vxx - _vyy) + (_ww * (lx + ly))) / r);
    run_speed(1, w1);
    run_speed(2, -w2);
    run_speed(3, w3);
    run_speed(4, -w4);
    //    debug.println("w1: " + String(w1) + ",w2: " + String(w2) + ",w3: " + String(w3) + ",w4: " + String(w4));
    long t2 = millis();
    countTa += (t2 - t1);
    tmp = (t2 - t1);
  }

  delay(_t * 1000);

  countTa = 0;
  tmp = 0;

  while (countTa <= _ta * 1000) {
    long t1 = millis();
    _vxx -= _ax * tmp / 1000;
    _vyy -= _ay * tmp / 1000;
    _ww -= _aw * tmp / 1000;

    w1 = degrees(((_vxx - _vyy) - (_ww * (lx + ly))) / r);
    w2 = degrees(((_vxx + _vyy) + (_ww * (lx + ly))) / r);
    w3 = degrees(((_vxx + _vyy) - (_ww * (lx + ly))) / r);
    w4 = degrees(((_vxx - _vyy) + (_ww * (lx + ly))) / r);
    run_speed(1, w1);
    run_speed(2, -w2);
    run_speed(3, w3);
    run_speed(4, -w4);
    //    debug.println("w1: " + String(w1) + ",w2: " + String(w2) + ",w3: " + String(w3) + ",w4: " + String(w4));
    long t2 = millis();
    countTa += (t2 - t1);
    tmp = (t2 - t1);
  }

  pidx = 0;
  pidy = 0;
  pidw = 0;

  run_speed(1, 0);
  run_speed(2, 0);
  run_speed(3, 0);
  run_speed(4, 0);
}

void find_object(){
  double ang_speed = 30;
  double errorCoreX, sCoreX, pCoreX, iCoreX, dCoreX, pre_errorCoreX, pidCoreX;


  sCoreX = 300;
  pidCoreX = 0;

  while (true) {
    if (detectionMode == 1) {
      errorCoreX = sCoreX - coreX;
      pCoreX = errorCoreX * kpy;
      iCoreX = kiy * (iCoreX + errorCoreX);
      dCoreX = kdy * (errorCoreX - pre_errorCoreX);
      pre_errorCoreX = errorCoreX;
      double correctpixx = pCoreX + iCoreX + dCoreX;
      pidCoreX = correctpixx;
      pidCoreX = _min(1500, pidCoreX);
      pidCoreX = _max(-1500, pidCoreX);

      w1 = degrees(((0 - pidCoreX) - (0 * (lx + ly))) / r);
      w2 = degrees(((0 + pidCoreX) + (0 * (lx + ly))) / r);
      w3 = degrees(((0 + pidCoreX) - (0 * (lx + ly))) / r);
      w4 = degrees(((0 - pidCoreX) + (0 * (lx + ly))) / r);
      run_speed(1, w1);
      run_speed(2, -w2);
      run_speed(3, w3);
      run_speed(4, -w4);
    } else {
      pidCoreX = 0;
      pCoreX = 0;
      iCoreX = 0;
      dCoreX = 0;
      pre_errorCoreX = 0;
      run_speed(1, 0);
      run_speed(2, 0);
      run_speed(3, 0);
      run_speed(4, 0);
    }

    if(errorCoreX > -10 && errorCoreX < 10 ){
      Serial.print("Ball Found");
      getBall = true;
      break;
    }
  }
}

void collect_ball() {
  float lastdepth = depth;
  servob.write(140);
  digitalWrite(pwmpin[4], 1);
  motorMotion(500, 0, 0, depth, 0, 1);
  while (digitalRead(inball_grip) == 0) {
//    motorMotion(200, 0, 0, 100, 0, 0.5);
//    lastdepth += 100;
    delay(10);
  }
  servob.write(45);
//  run_speed(1, 0);
//  run_speed(2, 0);
//  run_speed(3, 0);
//  run_speed(4, 0);
  digitalWrite(pwmpin[4], 0);
//  delay(2000);
  while (digitalRead(inball) == 0) {
    for (int i = 0; i < 5; i++) {
      digitalWrite(pwmpin[i], 1);
    }
    grip(true);
    delay(100);
  }
  for (int i = 0; i < 5; i++) {
    digitalWrite(pwmpin[i], 0);
  }
  grip(false);
  servob.write(140);
  motorMotion(-500, 0, 0, lastdepth, 0, 2);
  motorMotion(0, 0, 20, 0, 180, 2);
}
