// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Counter {
  mapping (bytes32 => uint32) private storeC;
  mapping (uint32 => bytes32) private R;
  uint32 private RClength;


  function get(string memory key)
  public view
  returns (uint32 value)
  {
    for (uint32 i = 0; i < RClength; i++) {
        bytes32 r = R[RClength - i];
        bytes32 hashedkey = keccak256(abi.encodePacked(key,r));
        if(storeC[hashedkey] > 0){
            return storeC[hashedkey];
        }
    }
    return 0;
  }

  function set(bytes32 key, bytes32 r, uint32 c)
  public
  {
    R[RClength] = r;
    storeC[key] = c;
    RClength ++;
  }
}