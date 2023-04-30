db = db.getSiblingDB("EchoNet");

db.createUser({
  user: "modelUser",
  pwd: "EchoNetAccess2023",
  roles: [
    {
      role: "readWrite",
      db: "EchoNet",
    },
  ],
});

db.createCollection("events");
db.createCollection("species");
db.createCollection("movements");
